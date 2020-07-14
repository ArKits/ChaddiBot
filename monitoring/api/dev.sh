set -e

echo "==> Building..."
go build -o chaddi-api main.go

echo "==> Running..."
./chaddi-api