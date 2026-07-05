if __name__ == "__main__":
    code = """
   
            co7.1 # CO:('cells<'startingCellsPointer'>' == 0);
            if7.1 # IF:co7.1;
            if7.1 ? START:1;
                loop2 ? STOP:;
            if7.1 ? END:;

            § ---- + ------ 
            co7.2 # CO:('code'=='charMap<1>');
            if7.2 # IF:co7.2;
            if7.2 ? START:2;
                mo1 # MO:(('cells' + 1) % 256);
                cells ? w:'mo1';
            if7.2 ? END:;

            § ---- - ------ 
            co7.3 # CO:('code'=='charMap<2>');
            if7.3 # IF:co7.3;
            if7.3 ? START:2;
                mo2 # MO:(('cells' - 1) % 256);
                cells ? w:'mo2';
            if7.3 ? END:;
            
            § ---- > ----- 
            co7.4 # CO:('code'=='charMap<3>');
            if7.4 # IF:co7.4;
            if7.4 ? START:2;
                cellsPointer ? w:++;
                cells ? SET:'cellsPointer';
            if7.4 ? END:;
            
            § ---- < ------ 
            co7.5 # CO:('code'=='charMap<4>');
            if7.5 # IF:co7.5;
            if7.5 ? START:2;
                cellsPointer ? w:--;
                cells ? SET:'cellsPointer';
            if7.5 ? END:;
        
            § ---- . ------ 
            co7.6 # CO:('code'=='charMap<5>');
            if7.6 # IF:co7.6;
            if7.6 ? START:3;
                char # PT:;
                ascii ? ToAscii:'cells'|char;
                output ? w:++|'char';
            if7.6 ? END:;
        
            § ---- , ------ 
            co7.7 # CO:('code'=='charMap<6>');
            if7.7 # IF:co7.7;
            if7.7 ? START:5;
                input # PT:;
                input ? INPUT:-> ;
                inputAsNum # INT:;
                ascii ? ToNum:'input'|inputAsNum;
                cells ? w:'inputAsNum';
            if7.7 ? END:;

            § ---- ] ----
            co8 # CO:('code'=='charMap<8>');
            if8 # IF:co8;
            if8 ? START:7;
                codePointer ? w:'startingCodePointer';
                code ? SET:'codePointer';

                co8.1 # CO:('cells<'startingCellsPointer'>'==0);
                if8.1 # IF:co8.1;
                if8.1 ? START:1;
                    loop2 ? STOP:;
                if8.1 ? END:;
            if8 ? END:;
    """
    
    count = 0
    for line in code.split("\n"):
        line = line.strip()
        if line and not line.startswith("§"):
            count += 1
    
    print(count)