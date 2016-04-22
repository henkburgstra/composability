package composability

import (
	"fmt"
	"testing"
)

func PassTransform(t ITransform) {
	fmt.Printf("success")
}

func TestTransformDate(t *testing.T) {
	x := NewTransformDate("22-08-1965")
	PassTransform(x)
}
