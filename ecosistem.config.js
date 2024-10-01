module.exports = {
    apps: [
      {
        name: "my-digital-system-api",
        script: "uvicorn",
        args: "main:app --host 0.0.0.0 --port 5000",
        exec_mode: "fork",
        autorestart: true,
        watch: false,
        max_restarts: 10,
      }
    ]
  };
  