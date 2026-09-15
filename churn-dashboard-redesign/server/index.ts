import express from "express";
import { createServer } from "http";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health / Status endpoint for Vercel / testing
app.get("/api/health", (_req, res) => {
  res.json({
    status: "healthy",
    service: "ChurnIQ API",
    environment: process.env.NODE_ENV || "development",
    timestamp: new Date().toISOString()
  });
});

// Serve static files from dist/public in production
const staticPath =
  process.env.NODE_ENV === "production"
    ? path.resolve(__dirname, "public")
    : path.resolve(__dirname, "..", "dist", "public");

app.use(express.static(staticPath));

// Handle client-side routing - serve index.html for non-API routes
app.get("*", (req, res, next) => {
  if (req.path.startsWith("/api/")) {
    return next();
  }
  res.sendFile(path.join(staticPath, "index.html"));
});

// Start standalone HTTP listener only when running outside Vercel serverless environment
if (!process.env.VERCEL && process.env.NODE_ENV !== "test") {
  const port = process.env.PORT || 3000;
  const server = createServer(app);
  server.listen(port, () => {
    console.log(`Server running on http://localhost:${port}/`);
  });
}

// Export app for @vercel/node serverless function handler
export default app;

// CommonJS compatibility bridge
if (typeof module !== "undefined" && module.exports) {
  module.exports = app;
}
