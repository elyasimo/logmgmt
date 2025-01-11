const { createServer } = require('http')
const { parse } = require('url')
const next = require('next')
const fs = require('fs')
const path = require('path')

const dev = process.env.NODE_ENV !== 'production'
const hostname = '0.0.0.0'
const port = 3000
const app = next({ dev, hostname, port })
const handle = app.getRequestHandler()

const logFile = path.join(__dirname, 'server.log')

// Create a write stream for logging
const logStream = fs.createWriteStream(logFile, { flags: 'a' })

// Custom logging function
function log(message) {
  const timestamp = new Date().toISOString()
  const logMessage = `${timestamp} - ${message}\n`
  console.log(logMessage)
  logStream.write(logMessage)
}

app.prepare().then(() => {
  createServer(async (req, res) => {
    try {
      const parsedUrl = parse(req.url, true)
      await handle(req, res, parsedUrl)
    } catch (err) {
      log(`Error occurred handling ${req.url}: ${err.message}`)
      res.statusCode = 500
      res.end('internal server error')
    }
  }).listen(port, hostname, (err) => {
    if (err) throw err
    log(`> Ready on http://${hostname}:${port}`)
  })
})

// Log unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  log(`Unhandled Rejection at: ${promise}, reason: ${reason}`)
})

// Log uncaught exceptions
process.on('uncaughtException', (error) => {
  log(`Uncaught Exception: ${error.message}`)
})

