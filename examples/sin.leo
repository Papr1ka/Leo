/*
	Программа для вычисления синуса угла, переданного в градусах
	Ввод: значение угла в градусах
	Вывод: синус угла
*/
{
	float angle;
	float sin;

	float sinn;    /* n-ое слагаемое ряда Тейлора */
	float powx;    /* x ^ (2n + 1)                */
	float factx;   /* (2n + 1)!                   */
	bool sinsign;  /* Знак синуса                 */

	readln angle;

	if (angle < 0.0)
	begin
		sinsign := true;
		angle := 0.0 - angle
	end
	else
		sinsign := false;

	/* Приведение угла к 1 четверти */
	while (angle >= 360.0)
		angle := angle - 360.0;
	if (angle >= 180.0)
	begin
		angle := angle - 180.0;
		sinsign := !sinsign
	end
	else if ((angle > 90.0) && (angle < 180.0))
		angle := 180.0 - angle;

	angle := angle * 3.141592653589 / 180.0;  /* Перевод в радианы */

	sin := 0.0;
	powx := angle;
	factx := 1.0;

	float nf;  /* Костыль для приведения типов */
	nf := 0.0;
	for n := 0 to 15
	begin
		sinn := powx / factx;
		if (sinn <= powx)  /* Проверка на NaN */
		begin
			if (n / 2 * 2 != n)
				sinn := sinn * (0.0 - 1.0);
			sin := sin + sinn;
			powx := powx * angle * angle;
			factx := factx * (2.0 * nf + 2.0) * (2.0 * nf + 3.0)
		end;
		nf := nf + 1.0
	end
	next;

	if (sinsign)
		sin := 0.0 - sin;

	writeln sin;
}
