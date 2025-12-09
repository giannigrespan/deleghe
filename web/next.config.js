/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  api: {
    bodyParser: {
      sizeLimit: '10mb', // Limite upload file
    },
  },
}

module.exports = nextConfig
