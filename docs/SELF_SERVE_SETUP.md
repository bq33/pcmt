# PCMT Self-Serve Setup Guide

Set up Personal Content Moderation Tool for your own Instagram account in about 15 minutes. No coding required.

## What You Need

- An Instagram Business or Creator account
- A Facebook account (to access Meta for Developers)
- 15 minutes

## Step 1: Create a Meta App

1. Go to https://developers.facebook.com/apps/
2. Click Create App
3. Select Business as the app type
4. Name it something like "PCMT - [Your Name]"
5. Click Create App

## Step 2: Add Instagram API

1. In your app dashboard, click Add Product
2. Find Instagram and click Set Up
3. Go to API Setup with Instagram Login

## Step 3: Connect Your Instagram Account

1. Under "API Setup with Instagram Login", click Add Account
2. Log in with your Instagram Business/Creator account
3. Accept the tester invitation (check your Instagram app under Settings > Apps and Websites)

## Step 4: Configure Webhooks

1. In your Meta app, go to the Instagram product > Webhooks (or API Setup > Configure Webhooks)
2. Set Callback URL to your PCMT instance: https://your-pcmt-instance.fly.dev/webhook
3. Set Verify Token to the value provided by your PCMT host
4. Click Verify and Save
5. Subscribe to the comments field (toggle it ON)

## Step 5: Generate an Access Token

1. In API Setup with Instagram Login, find Generate Token
2. Select your Instagram account
3. Copy the token — you'll need it for PCMT configuration

## Step 6: Configure PCMT

Provide these three values to your PCMT instance:

- PCMT_VERIFY_TOKEN: The verify token you set in Step 4
- PCMT_APP_SECRET: Found in your Meta app under Settings > Basic > App Secret (click Show)
- PCMT_ACCESS_TOKEN: The token from Step 5

Your host will configure these as environment variables and restart the service.

## Step 7: Test It

1. Have someone comment on one of your Instagram posts
2. Check your PCMT logs — you should see the comment event
3. PCMT will automatically moderate based on your policy

## Troubleshooting

Webhooks not arriving?
- Verify your app is in Development mode (this is fine for your own account)
- Make sure your Instagram account accepted the tester invitation
- Check that the Callback URL is correct and reachable
- The verify token must match exactly

Signature errors in logs?
- The App Secret on your PCMT instance must match the one in your Meta app Settings > Basic
- If you reset the App Secret, update it on your PCMT instance
