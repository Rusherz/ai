const fs = require('fs');


let content = fs.readFileSync('./results.json', 'utf8');

content = content.replace(/'/g, '"');

content = JSON.parse(content);

let dois = [];

for (let entity in content['entities']) {
    console.log(entity);
}