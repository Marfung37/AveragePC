const fs = require("fs");
const hashmap = require("hashmap");
const {decoder} = require('tetris-fumen');

var fumenCodes = process.argv.slice(2);

for(let code of fumenCodes){
    let pages = decoder.decode(code);
    let pieceCounts = new hashmap()
    pieceCounts.multi("T", 0, "I", 0, "L", 0, "J", 0, "S", 0, "Z", 0, "O", 0)
    let pieces = "";
    // unglued fumen
    if(pages.length == 1){
        let page = pages[0];
        let field = page.field.str().split("\n").slice(0,-1);
        for(let line of field){
            for(let p of pieceCounts.keys()){
                pieceCounts.set(p, pieceCounts.get(p) + line.split(p).length - 1);
            }
        }

        for(let p of pieceCounts.keys()){
            pieces += p.repeat(pieceCounts.get(p) / 4)
        }
    }
    // glued fumen
    else{
        for(let i in pages){
            pieceCounts.set(pages[i].operation.type, pieceCounts.get(pages[i].operation.type) + 1);
        }
        for(let p of pieceCounts.keys()){
            pieces += p.repeat(pieceCounts.get(p));
        }
    }

    console.log(pieces);
}