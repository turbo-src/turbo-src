# How to update the api

## File that must be updated

1. service/server.js - graphQL schema

2. service/src/utils/requests.js

3. service/src/utils/<subService>/Requests.js

4. <subService>/server/index.js - graphQL schema

5. <subService>/src/request.js - graphQL schema

<subService>/lib/index.js - add related function to export if a new endpoint.