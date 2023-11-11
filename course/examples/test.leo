{
    int i;
    float number, current;
    int j;

    readln number;

    current := number;

    for i := 1 to 11 step 1
    begin

        current := current * number;
        writeln current
    end
    next;
}