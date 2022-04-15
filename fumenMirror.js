const {encoder, decoder, Field} = require('tetris-fumen');
const Hashmap = require('hashmap');

function reverse(value) {  
    return Array.from(
      String(value || '')
    ).reverse().join('')
}

const pieceMirror = new Hashmap();
pieceMirror.set("L", "J");
pieceMirror.set("J", "L");
pieceMirror.set("S", "Z");
pieceMirror.set("Z", "S");

var fumenCodes = process.argv.slice(2);
for(let code of fumenCodes){
    let page = decoder.decode(code)[0];
    let field = page.field.str().split("\n").slice(0,-1);
    let newLines = [];
    for(let line of field){
        let reversedLine = reverse(line);
        let newL = "";
        for(let m of reversedLine){
            if(pieceMirror.has(m)){
                newL += pieceMirror.get(m);
            }
            else{
                newL += m;
            }
        }
        newLines.push(newL);
    }

    let newField = Field.create(newLines.join(""));
    let pages = [];
    pages.push({field: newField})
    let newFumen = encoder.encode(pages);

    console.log(newFumen);
}
