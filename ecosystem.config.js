module.exports = {
  apps: [
    {
      name: "my-digital-system-api",
      script: "uvicorn",
      args: "main:app --host 0.0.0.0 --port 5000",
      interpreter: "venv/bin/python",
      autorestart: true,
      watch: false,
    }
  ]
};
