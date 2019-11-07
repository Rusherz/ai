const fs = require('fs');


let content = fs.readFileSync('./names.txt', 'utf8');

let lines = content.split('\n');

let dataLines = [];
let trainingData = [
    'File, Line, Begin Offset, End Offset, Type'
];

for (let index in lines) {
    if (!lines[index]) {
        continue;
    }

    let [sentence, name] = lines[index].split(':::');

    let beginOffset = sentence.indexOf(name);
    let endOffset = beginOffset + name.length;

    dataLines.push(sentence);
    trainingData.push(`data.txt, ${index}, ${beginOffset}, ${endOffset}, APPLICATION`);
}

fs.writeFileSync('./data.txt', dataLines.join('\n'));
fs.writeFileSync('./training.txt', trainingData.join('\n'));