const fs = require('fs');


let content = fs.readFileSync('./ner_dataset.csv', 'utf8');
let dois = fs.readFileSync('./doi.txt', 'utf8');

let lines = content.split('\n');
dois = dois.split('\n');

let dataLines = [];

for (let index in lines) {
    if (!lines[index]) {
        continue;
    }

    if (lines[index] == ',.,.,O' || lines[index].indexOf('Sentence: ') != -1) {
        dataLines.push(lines[index]);
        continue;
    }

    if (Math.random() > 0.9) {
        console.log(`,${dois[Math.floor(Math.random() * dois.length)]},NNS,DOI`)
        dataLines.push(`,${dois[Math.floor(Math.random() * dois.length)]},NNS,DOI`);
    }

    dataLines.push(lines[index]);
}

fs.writeFileSync('./data.txt', dataLines.join('\n'));