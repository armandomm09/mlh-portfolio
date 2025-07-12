#!/usr/bin/env bash

# Generate random data
RAND=$RANDOM
NAME="User${RAND}"
EMAIL="user${RAND}@example.com"
CONTENT="Test content ${RAND}"

API_BASE="http://armando-mlh-portfolio.duckdns.org:5000/api/timeline_post"

echo "Creating timeline post with:"
echo "  name:    $NAME"
echo "  email:   $EMAIL"
echo "  content: $CONTENT"
echo

# POST to create a new timeline post
POST_RESPONSE=$(curl -s -X POST "$API_BASE" \
  -d "name=${NAME}" \
  -d "email=${EMAIL}" \
  -d "content=${CONTENT}")

echo "POST Response:"
echo "$POST_RESPONSE"
echo

# GET to verify the post was created
GET_RESPONSE=$(curl -s "$API_BASE")

echo "GET Response (latest posts):"
echo "$GET_RESPONSE" | jq .
echo

# Verify that the GET contains our content
if echo "$GET_RESPONSE" | grep -qF "$CONTENT"; then
  echo "Test passed: the content was found in the GET response."
  exit 0
else
  echo "Test failed: the content was NOT found in the GET response."
  exit 1
fi
