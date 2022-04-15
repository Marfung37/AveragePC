# AveragePC
Get the average of inputted set of setups based on coverage and score  

## Dependencies
```npm install tetris-fumen``` - fumen api  
```npm install hashmap``` - hashmap

## Run command
```python avgPercent```
Mirror prompt - also include the mirror of setups  
  * y if pieces for setup (-p) is the same for either direction of setup  
Glued prompt - the fumens in setups.csv are already glued  
Fractions prompt - the scoring in represented as a fraction rather than a percent in setup.csv  

## Input File - setup.csv
The format of the file is `fumen score [pieces after]`  
`fumen` - fumen of setups can be unglued or glued (state in glued prompt)  
`score` - score for setup  
`[pieces after]` - (optional) sfinder format for pieces that must be after the setup to be covered  

## Output files
percentOut - file that includes what setup is best for each queue  
lastOut - file that includes priority coverage, average percent/fraction, and queues not covered  
