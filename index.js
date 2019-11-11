const fs = require('fs');


let content = fs.readFileSync('./results.json', 'utf8');

//content = content.replace(/'/g, '"');

content = JSON.parse(content);

let dois = content.entities.filter(entity => {
    return entity.type == ' DOI'
});

console.log(dois)