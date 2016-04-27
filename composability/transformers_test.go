package composability

import (
	"fmt"
	"testing"
)

func PassTransform(t ITransform) {
	fmt.Println("PassTransform: success")
}

func TestTransformDate(t *testing.T) {
	x := NewTransformDate("22-08-1965")
	PassTransform(x)
}

func TestTransformDateDisplay(t *testing.T) {
	d := "22-08-1965"
	x := NewTransformDate(d)
	d2 := x.Display()
	if d != d2 {
		t.Errorf("Display is '%s', expected '%s'", d2, d)
	}
}

func TestTransformDateStore(t *testing.T) {
	d := "1965-08-22"
	x := NewTransformDate("22-08-1965")
	d2 := x.Store()
	if d != d2 {
		t.Errorf("Display is '%s', expected '%s'", d2, d)
	}
}
