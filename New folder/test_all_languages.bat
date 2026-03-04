@echo off
:: =======================
:: Multi-Language API Test
:: =======================

:: Base URL
set URL=http://localhost:10001/run

:: -----------------------
:: Python
curl -X POST %URL% -H "Content-Type: application/json" -d "{\"language\":\"python\",\"code\":\"print('Hello Python')\"}"
echo.

:: -----------------------
:: C
curl -X POST %URL% -H "Content-Type: application/json" -d "{\"language\":\"c\",\"code\":\"#include <stdio.h>\nint main(){printf(\\\"Hello C\\\");return 0;}\"}"
echo.

:: -----------------------
:: C++
curl -X POST %URL% -H "Content-Type: application/json" -d "{\"language\":\"c++\",\"code\":\"#include <iostream>\nusing namespace std;\nint main(){cout<<\\\"Hello C++\\\"; return 0;}\"}"
echo.

:: -----------------------
:: Java
curl -X POST %URL% -H "Content-Type: application/json" -d "{\"language\":\"java\",\"code\":\"public class Program { public static void main(String[] args){System.out.println(\\\"Hello Java\\\");} }\"}"
echo.

:: -----------------------
:: JavaScript
curl -X POST %URL% -H "Content-Type: application/json" -d "{\"language\":\"javascript\",\"code\":\"console.log('Hello JavaScript')\"}"
echo.

:: -----------------------
:: PHP
curl -X POST %URL% -H "Content-Type: application/json" -d "{\"language\":\"php\",\"code\":\"<?php echo 'Hello PHP'; ?>\"}"
echo.

:: -----------------------
:: Go
curl -X POST %URL% -H "Content-Type: application/json" -d "{\"language\":\"go\",\"code\":\"package main\nimport \\\"fmt\\\"\nfunc main(){fmt.Println(\\\"Hello Go\\\")}\"}"
echo.

:: -----------------------
:: Kotlin
curl -X POST %URL% -H "Content-Type: application/json" -d "{\"language\":\"kotlin\",\"code\":\"fun main() { println(\\\"Hello Kotlin\\\") }\"}"
echo.

:: -----------------------
:: Rust
curl -X POST %URL% -H "Content-Type: application/json" -d "{\"language\":\"rust\",\"code\":\"fn main(){println!(\\\"Hello Rust\\\");}\"}"
echo.

:: -----------------------
:: R
curl -X POST %URL% -H "Content-Type: application/json" -d "{\"language\":\"r\",\"code\":\"cat('Hello R\\n')\"}"
echo.