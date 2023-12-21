package utils

func PointerTo[T any](val T) *T {
	return &val
}
