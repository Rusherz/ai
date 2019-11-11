const fs = require('fs');


// let content = fs.readFileSync('./results.json', 'utf8');
//
// //content = content.replace(/'/g, '"');
//
// content = JSON.parse(content);
//
// let dois = content.entities.filter(entity => {
//     return entity.type == ' DOI'
// });
//
// console.log(dois)

let dois = fs.readFileSync('./doi.txt', 'utf8');
dois = dois.split("\n");

let newDois = [];

let count = parseInt(dois.length / 10) + 1;

for (let i = 0; i < count; i++) {
    for (let o = 0; o < 10; o++) {
        newDois.push(dois[o + (10 * i)]);
    }
    newDois.push("\n");
}

fs.writeFileSync('./dois.txt', newDois.join('\n'));