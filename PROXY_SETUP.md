# Proxy Setup Guide

If GitHub Actions is being blocked, you can use a proxy to bypass IP restrictions.

## Option 1: Add Proxy to GitHub Secrets

1. Go to: https://github.com/UNcreator1/browser-use-auto/settings/secrets/actions
2. Add a new secret:
   - Name: `PROXY_URL`
   - Value: `http://proxy-server:port` or `http://user:pass@proxy-server:port`

## Option 2: Free Proxy Services

### WebShare (Recommended)
- URL: https://www.webshare.io/
- Free tier: 10 proxies
- Format: `http://username:password@proxy.webshare.io:port`

### ProxyScrape
- URL: https://proxyscrape.com/free-proxy-list
- Free public proxies (less reliable)

### Proxy-List
- URL: https://www.proxy-list.download/
- Free HTTP/SOCKS proxies

## How to Use

### Method 1: Environment Variable
```bash
export PROXY_URL="http://proxy.example.com:8080"
```

### Method 2: GitHub Secret
Add `PROXY_URL` secret, then the workflow will use it automatically.

## Testing Proxy

Test if proxy works:
```bash
curl -x http://proxy:port https://www.vietnamworks.com
```

## Current Status

The automation will:
1. Try without proxy first
2. If connection fails, suggest using proxy
3. You can add proxy support if needed

## Note

- Free proxies are often slow and unreliable
- Paid proxies ($5-10/month) are more stable
- Residential proxies work best for job sites
