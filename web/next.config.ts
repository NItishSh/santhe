import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains',
          },
          // Content-Security-Policy can be tricky with Next.js scripts (Safe 'unsafe-inline' for dev often needed)
          // Adding a basic tight policy, user may need to relax it for specific 3rd parties
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:;",
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          }
        ],
      },
    ];
  },
  async rewrites() {
    return [
      {
        source: '/api/users/:path*',
        destination: `${process.env.USER_SERVICE_URL || 'http://user-service:8000/api'}/users/:path*`,
      },
      {
        source: '/api/auth/:path*',
        destination: `${process.env.USER_SERVICE_URL || 'http://user-service:8000/api'}/auth/:path*`,
      },
      {
        source: '/api/products/:path*',
        destination: `${process.env.PRODUCT_SERVICE_URL || 'http://product-catalog-service:8000/api'}/products/:path*`,
      },
      {
        source: '/api/categories/:path*',
        destination: `${process.env.PRODUCT_SERVICE_URL || 'http://product-catalog-service:8000/api'}/categories/:path*`,
      },
    ];
  },
};



export default nextConfig;
