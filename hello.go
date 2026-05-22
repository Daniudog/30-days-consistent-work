// Create a for loop that goes from 100 to 0
// what is the difference between var and :=
// researh on function vs blocked scope variables in go and explain it to me
// What is a constant
// creat some vaariables and specifu their types
// build a calculator
package main

import "fmt"

func main() {
	a := 100
	for a >= 0 {
		fmt.Println(a)
		a = a - 1
	}
	for o := range 3 {
		fmt.Println(o)
	}
	for e := range 33 {
		if e-3 == 27 {
			continue
		}
		break
	}

	lmao()
	addition(k, c)
	subtraction(f, g)
	multiplication(y, z)
}

var ivan string = "jumping + is + fun"
var joy int = 12
var ups bool = false

func lmao() {
	fmt.Println(ivan)
	fmt.Println(joy)
	fmt.Println(ups)

}

var k int = 8
var c int = 5
var f int = 7
var g int = 2
var y int = 4
var z int = 3

func addition(k int, c int) int {
	return k + c
}

func subtraction(f int, g int) int {
	return f - g
}

func multiplication(y int, z int) int {
	return y * z
}
