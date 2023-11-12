{
    int n;
    int factorial;

    readln n;
    factorial := 1;

    while (n > 1)
    begin
        factorial := factorial * n;
        n := n - 1
    end;
    
    writeln factorial;
}