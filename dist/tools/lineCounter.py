if __name__ == "__main__":
    code = """
    cmd # PT:'code<'ip'>;
        
        
        § ---- + ------ 
        co1 # CO:('cmd'=='charMap<1>');
        if1 # IF:co1;
        if1 ? START:2;
            mo1 # MO:(('cells' + 1) % 256);
            cells ? w:'mo1';
        if1 ? END:;
    
        § ---- - ------ 
        co2 # CO:('code'=='charMap<2>');
        if2 # IF:co2;
        if2 ? START:2;
            mo2 # MO:(('cells' - 1) % 256);
            cells ? w:'mo2';
        if2 ? END:;
        
        § ---- > ----- 
        co3 # CO:('code'=='charMap<3>');
        if3 # IF:co3;
        if3 ? START:2;
            ptr ? w:++;
            cells ? SET:'ptr';
        if3 ? END:;
        
        § ---- < ------ 
        co4 # CO:('code'=='charMap<4>');
        if4 # IF:co4;
        if4 ? START:2;
            ptr ? w:--;
            cells ? SET:'ptr';
        if4 ? END:;
    
        § ---- . ------ 
        co5 # CO:('code'=='charMap<5>');
        if5 # IF:co5;
        if5 ? START:3;
            char # PT:;
            ascii ? ToAscii:'cells'|char;
            char ? push:;
        if5 ? END:;
    
        § ---- , ------ 
        co6 # CO:('code'=='charMap<6>');
        if6 # IF:co6;
        if6 ? START:5;
            input # PT:;
            input ? INPUT:-> ;
            inputAsNum # INT:;
            ascii ? ToNum:'input'|inputAsNum;
            cells ? w:'inputAsNum';
        if6 ? END:;
    
        § ---- [ ------ 
        co7 # CO:('code'=='charMap<7>');
        if7 # IF:co7;
        if7 ? START:5;
            co7.1 # CO:('cells'==0)
            if7.1 # IF:co7.1;
            if7.1 ? START: ;
                ip ? w:'bracketMap<'ip'>;
            if7.1 ? END:;
        if7 ? END:;
        
        § ---- ] ------ 
        co8 # CO:('code'=='charMap<8>');
        if8 # IF:co8;
        if8 ? START:5;
            co8.1 # CO:('cells'!=0)
            if8.1 # IF:co8.1;
            if8.1 ? START: ;
                ip ? w:'bracketMap<'ip'>;
            if8.1 ? END:;
        if8 ? END:;
    
        ip ? w:++;
    """
    
    count = 0
    for line in code.split("\n"):
        line = line.strip()
        if line and not line.startswith("§"):
            count += 1
    
    print(count)