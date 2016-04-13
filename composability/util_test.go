package composability

import (
	"testing"
)

func TestStripKey(t *testing.T) {
	for _, p := range []string{"path(1)/with(2)/keys", "path(a)/with(b)/keys", "path(a-1)/with(b-2)/keys"} {
		if StripKey(p) != "path/with/keys" {
			t.Error(StripKey(p), " != ", "path/with/keys")
		}
	}
}
