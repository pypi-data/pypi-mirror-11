disp('non blocking behaviour')
[fin, fout, pid] = popen2("cat", {}, false);
fputs(fin, "hello world");
fflush(fin);
msg = fgetl(fout)

disp('blocking behaviour')
fflush(stdout)
[fin, fout, pid] = popen2("cat", {}, true);
fputs(fin, "hello world");
fflush(fin);
msg = fgetl(fout)

