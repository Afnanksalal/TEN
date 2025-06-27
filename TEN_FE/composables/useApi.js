
 // composables/useApi.js
 // For Nuxt 3 composables, useRuntimeConfig is auto-imported,
 // but explicit import often helps if issues persist.
 // import { useRuntimeConfig } from '#app'; // This import might be needed if not auto-resolving

 export function useApi() {
   const runtimeConfig = useRuntimeConfig();

   // VERIFY THESE VALUES by adding console.log here:
   // console.log("API_BASE_URL from runtimeConfig:", runtimeConfig.public.apiBaseUrl);
   // console.log("BACKEND_API_KEY from runtimeConfig:", runtimeConfig.public.backendApiKey);

   const API_BASE_URL = runtimeConfig.public.apiBaseUrl;
   const BACKEND_API_KEY = runtimeConfig.public.backendApiKey;

   const callApi = async (endpoint, method = 'POST', payload = null, headers = {}) => { // Changed default method to POST for this context
     // VERIFY THE CONSTRUCTED URL:
     // console.log("Constructed API URL:", `${API_BASE_URL}${endpoint}`);
     const url = `${API_BASE_URL}${endpoint}`;

     const defaultHeaders = {
       'Content-Type': 'application/json',
       'Accept': 'application/json',
       'X-API-Key': BACKEND_API_KEY,
       ...headers,
     };

     const options = {
       method,
       headers: defaultHeaders,
     };

     if (payload && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
       options.body = JSON.stringify(payload);
     }

     try {
       const response = await fetch(url, options);
       const data = await response.json();

       if (!response.ok) {
         let errorMessage = `API Error: ${response.status}`;
         if (data.detail) {
           errorMessage += ` - ${typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)}`;
         } else if (data.error_message) {
           errorMessage += ` - ${data.error_message}`;
         } else {
           errorMessage += ` - Unknown error`;
         }
         if (response.status === 429) {
           errorMessage = 'Too many requests. Please try again later.';
         } else if (response.status === 401) {
           errorMessage = 'Authentication failed. Invalid API Key.';
         } else if (response.status === 403) {
           errorMessage = 'Access denied.';
         }
         const error = new Error(errorMessage);
         error.status = response.status;
         error.data = data;
         throw error;
       }

       return data;
     } catch (err) {
       if (err instanceof TypeError && err.message.includes('Failed to fetch')) {
         throw new Error('Network error or server unreachable. Please check your internet connection or try again later.');
       }
       throw err;
     }
   };

   return {
     callApi,
   };
 }
 