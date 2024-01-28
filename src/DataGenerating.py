from random import uniform

for _index in range(1, 1001):
    Random = ["{:.2f}".format(round(uniform(100, 250), 2)) for _ in range(30)]
    File = open(f"../public/data/raw_data/Flows/{_index}", 'w')
    File.write(f"DEMANDS (\n  AB ( A B ) 1 {Random[0]}\n  BA ( B A ) 1 {Random[1]}\n  AC ( A C ) 1 {Random[2]}\n  CA ( C A ) 1 {Random[3]}\n  AD ( A D ) 1 {Random[4]}\n  DA ( D A ) 1 {Random[5]}\n  AE ( A E ) 1 {Random[6]}\n  EA ( E A ) 1 {Random[7]}\n  AF ( A F ) 1 {Random[8]}\n  FA ( F A ) 1 {Random[9]}\n  BC ( B C ) 1 {Random[10]}\n  CB ( C B ) 1 {Random[11]}\n  BD ( B D ) 1 {Random[12]}\n  DB ( D B ) 1 {Random[13]}\n  BE ( B E ) 1 {Random[14]}\n  EB ( E B ) 1 {Random[15]}\n  BF ( B F ) 1 {Random[16]}\n  FB ( F B ) 1 {Random[17]}\n  CD ( C D ) 1 {Random[18]}\n  DC ( D C ) 1 {Random[19]}\n  CE ( C E ) 1 {Random[20]}\n  EC ( E C ) 1 {Random[21]}\n  CF ( C F ) 1 {Random[22]}\n  FC ( F C ) 1 {Random[23]}\n  DE ( D E ) 1 {Random[24]}\n  ED ( E D ) 1 {Random[25]}\n  DF ( D F ) 1 {Random[26]}\n  FD ( F D ) 1 {Random[27]}\n  EF ( E F ) 1 {Random[28]}\n  FE ( F E ) 1 {Random[29]}\n)\n")
