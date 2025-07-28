// make an api call to makcorps.com

url = "https://api.makcorps.com/city";

apiKey = "6739d80fee828d915fb4e154";
const response = await fetch(url + apiKey);
const data = await response.json();

console.log(data);
