@echo off
IF [%JUSTTERMINATE%] == [OKAY] (
    SET JUSTTERMINATE=
    python qttmwirc.py %*
) ELSE (
    SET JUSTTERMINATE=OKAY
    CALL %0 %* <NUL
)