/**
 * Production-Ready Express Rate Limiting Middleware
 * NIST Control: AC-7 (Unsuccessful Logon Attempts)
 */

const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const redis = require('redis');

const redisClient = redis.createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379'
});

redisClient.connect();

const globalRateLimiter = rateLimit({
  store: new RedisStore({ client: redisClient, prefix: 'rl:global:' }),
  windowMs: 15 * 60 * 1000,
  max: 1000,
  handler: (req, res) => {
    res.status(429).json({
      error: 'too_many_requests',
      message: 'Too many requests from this IP',
      retry_after: 900
    });
  }
});

const userRateLimiter = rateLimit({
  store: new RedisStore({ client: redisClient, prefix: 'rl:user:' }),
  windowMs: 60 * 1000,
  max: 100,
  keyGenerator: (req) => req.user?.id || req.ip
});

function createEndpointLimiter(maxRequests, windowMinutes, name) {
  return rateLimit({
    store: new RedisStore({ client: redisClient, prefix: `rl:${name}:` }),
    windowMs: windowMinutes * 60 * 1000,
    max: maxRequests
  });
}

module.exports = { globalRateLimiter, userRateLimiter, createEndpointLimiter };
