# Array

Array class used to store collection of objects of the same type.

## Construction

```ts
    let array = new Array([1, 2, 3])
```

## Static methods

### `Array.from`

Creates a new Array from an array of Object or String.

```ts
    const array1 = Array.from([1, 2, 3])
    const array2 = Array.from("abc")
    const array3 = Array.from([3.2, 4.3, 9.1])
    
    console.log(array1)
    // expected output: [1, 2, 3]
    console.log(array2)
    // expected output: ["a", "b", "c"]
    console.log(array3)
    // expected output: [3.2, 4.3, 9.1]
```

### `Array.of`

Create a new Array from variable number of arguments.

```ts
    const array1 = Array.of(1, 2, 3)
    const array2 = Array.of("foo", "bar")

    console.log(array1)
    // expected output: [1, 2, 3]
    console.log(array2)
    // expected output: ["foo", "bar"]

```

## Instance properties

### `Array.length`

Specifies the length of the array.

```ts
    const array = new Array([1, 2, 3])
    console.log(array.length)
    // expected output: 3
```

## Instance methods

### `Array.at`

Returns the object at the given index of the array.

```ts
    const array = new Array([8, -2, 12])
    console.log(array.at(0))
    // expected output: 8
    console.log(array.at(2))
    // expected output: 12
```

### `Array.concat`

Returns the concatenation of two arrays as a new array. Doesn't modify the original array.

```ts
    const array1 = new Array(["hello", "this"])
    const array2 = new Array(["beautiful", "world"])
    const array3 = array1.concat(array2)
    console.log(array3)
    // expected output: ["hello", "this", "beautiful", "world"]
```

### `Array.copyWithin`

Used to copy a sequence of elements within an array and paste them to a new location.
This method modifies the original array and returns it. 

```ts
    let array1 = new Array([1, 2, 3, 4, 5])
    array1.copyWithin(0, 3)
    console.log(array1) 
    // expected output: [4, 5, 3, 4, 5]
```

### `Array.entries`

TODO: iterator

### `Array.every`

Returns a boolean value indicating whether every element in the array satisfies passed condition

```ts
    const array = new Array([1, 2, 3, 4, 5])
    console.log(array.every(n => n < 10))
    // expected output: true
```

### `Array.fill`

Changes values of an array to specified value according to the specified start and end positions.
Modifies the array and returns it's copy.

```ts
    let array = new Array([-2, -1, 0, 1, 2])
    array.fill(100, 1, 3)
    console.log(array)
    // expected output: [-2, 100, 100, 1, 2]
    array.fill(0)
    // expected output: [0, 0, 0, 0, 0]
```

### `Array.filter`

Filters an array using the specified predicate function. Does not modify the array.

```ts
    const array = new Array(["some", "random", "words"])
    const result = array.filter(x => x != "random")
    console.log(result)
    // expected output: ["some", "words"]
```

### `Array.find`

Finds the first element of the array matching the specified predicate

TODO: no undefined

### `Array.findIndex`

Finds an index of the first element of the array matching the specified predicate.
Returns -1 if no such element present.

```ts
    const array = new Array(["hello", "world", "!"])
    const result = array.findIndex(x => x == "!")
    console.log(result)
    // expected output: 2
```

### `Array.flat`

Returns a new array as a result of concatenating all nested arrays. Specified parameter used to indicate the depth to which concatenation is perfomed.

```ts
    const array1 = new Array([0, 2, [3, 5, [0, 12]]])
    const result1 = array1.flat()
    console.log(result1)
    // expected output: [0, 2, 3, 5, 0, 12]

    const array2 = new Array(["def", ["sq", "x"], ["body", ["*", "x", "x"]]])
    const result2 = array.flat(2)
    console.log(result2)
    // expected output: ["def", "sq", "x", "body", "*", "x", "x"]
```

### `Array.flatMap`

Behaves similarly to `Array.map`, but flattens resulted array by one level.

```ts
    const array = new Array([0, 2, [3, 5, [0, 12]]])
    const result = array.flatMap(x => x)
    console.log(result)
    // expected output: [0, 2, 3, 5, [0, 12]]
```

### `Array.forEach`

Applies specified function for each element of the array. Does not return anything and does not modify the array.

```ts
    const array = new Array([1, 2, 3, 4, 5])
    numbers.forEach(x => console.log(x))
    // expected output: 1 2 3 4 5
```

### `Array.group`

TODO

### `Array.groupToMap`

TODO

### `Array.includes`

Returns true if provided value exists in the array, else otherwise.

```ts
    const array = new Array(["some", "strings"])
    console.log(array.includes("hello"))
    // expected output: false
```

### `Array.indexOf`

Similar to Array.findIndex, but uses equality to test elements

```ts
    const array = new Array(["here", "are", "some", "words"])
    const index = array.indexOf("are")
    console.log(index)
    // expected output: 1

    const neg_index = array.indexOf("hello")
    console.log(neg_index)
    // expected output: -1
```

### `Array.join`

Joins array elements with specified separator, using toString method on every element of array.
If no separator is provided, default separator "," (comma) is used.

```ts
    const array1 = new Array(["some", "body"])
    const joined1 = array1.join("...")
    console.log(joined1)
    // expected output: some...body

    const array2 = new Array([1, 2, 3, 4])
    const joined2 = array2.join("")
    console.log(joined2)
    // expected output: 1234
```

### `Array.keys` 

TODO: iterator

### `Array.lastIndexOf`

Array is searched backwards, starting from provided fromIndex and index of found element is returned.
If no element is found, returns -1.

```ts
    const array = new Array(["a", "b", "c", "c", "d"])
    const index = array.indexOf("c")
    console.log(index)
    // expected output: 3

    const neg_index = array.indexOf("z")
    console.log(neg_index)
    // expected output: -1
```

### `Array.map`

Creates new array, containing results of application of provided function to each element of array.

```ts
    const array = new Array([1, 2, 3, 4])
    const powers_of_two = array.map(x => 2 ** x)
    console.log(powers_of_two)
    // expected output: [2, 4, 8, 16]
```

# TypedArray

`TypedArray` object represents an array-like view of an underlying binary data buffer.
There is no `TypedArray` type, but a collection of types named according to the to different representations of the underlying binary data:

+ `Int8Array, Uint8Array, Uint8ClampedArray`: 8-bit signed and unsigned integers, and unsigned integers clamped to 0-255.
+ `Int16Array, Uint16Array`: 16-bit signed and unsigned integers.
+ `Int32Array, Uint32Array`: 32-bit signed and unsigned integers.
+ `Float32Array, Float64Array`: 32-bit and 64-bit floating-point numbers.
+ `BigInt64Array, BigUint64Array`: 64-bit signed and unsigned integers.

All `TypedArray` types and their instances have same API.

## Static properties

### `TypedArray.BYTES_PER_ELEMENT`

Represents the size in bytes of each element in a typed array.

```ts
    console.log(Int8Array.BYTES_PER_ELEMENT)
    // expected output: 1
    console.log(Float32Array.BYTES_PER_ELEMENT)
    // expected output: 4
    console.log(BigInt64Array.BYTES_PER_ELEMENT)
    // expected output: 8
```

## Static methods

### `TypedArray.from`

Creates a new TypedArray from an array of Object or String.

```js
    const array1 = Int8Array.from([1, 2, 3])
    const array2 = Float32Array.from("135")
    
    console.log(array1)
    // expected output: [1, 2, 3]
    console.log(array2)
    // expected output: ["1", "3", "5"]
```

### `TypedArray.of`

Create a new TypedArray from variable number of arguments.

```ts
    const array1 = Int8Array.of(1, 2, 3)
    const array2 = BigInt64Array.of(9843912058125, 0)

    console.log(array1)
    // expected output: [1, 2, 3]
    console.log(array2)
    // expected output: [9843912058125, 0]

```

## Instance properties

### `TypedArray.length`

Specifies the length (in elements) of the array.

```ts
    const array = new Int8Array([1, 2, 3])
    console.log(array.length)
    // expected output: 3
    const array = new Float64Array([3.5, 6.2])
    console.log(array.length)
    // expected output: 2
```

### `TypedArray.byteLength`

Specifies the length (in bytes) of the array.

```ts
    const array = new Int16Array([1, 2, 3])
    console.log(array.byteLength)
    // expected output: 6
    const array = new Float64Array([3.5, 6.2])
    console.log(array.byteLength)
    // expected output: 16
```

## Instance methods

### `TypedArray.at`

Returns the object at the given index of the array.

```ts
    const array = new Int8Array([8, -2, 127])
    console.log(array.at(0))
    // expected output: 8
    console.log(array.at(2))
    // expected output: 127
```

### `TypedArray.copyWithin`

Used to copy a sequence of elements within an array and paste them to a new location.
This method modifies the original array and returns it. 

```ts
    let array1 = new Int16Array([1, 2, 3, 4, 5])
    array1.copyWithin(0, 3)
    console.log(array1) 
    // expected output: [4, 5, 3, 4, 5]
```
### `TypedArray.every`

Returns a boolean value indicating whether every element in the array satisfies passed condition

```ts
    const array = new Int8Array([-2, -4, -5])
    console.log(array.every((n: int) => n > 0))
    // expected output: false
```

### `TypedArray.fill`

Changes values of an array to specified value according to the specified start and end positions.
Modifies the array and returns it's copy.

```ts
    let array = new Int32Array([-2, -1, 0, 1, 2])
    array.fill(100, 1, 3)
    console.log(array)
    // expected output: [-2, 100, 100, 1, 2]
    array.fill(0)
    // expected output: [0, 0, 0, 0, 0]
```

### `TypedArray.filter`

Filters an array using the specified predicate function. Does not modify the array.

```ts
    const array = new Int8Array([0, -2, 2])
    const result = array.filter(x => x > 0)
    console.log(result)
    // expected output: [2]
```

### `TypedArray.find`

Finds the first element of the array matching the specified predicate

TODO: iterator

### `TypedArray.findIndex`

Finds an index of the first element of the array matching the specified predicate.
Returns -1 if no such element present.

```ts
    const array = new Uint32Array([0, 12, 42, 101])
    const result = array.findIndex(x => x <= 42)
    console.log(result)
    // expected output: 0
```

### `TypedArray.forEach`

Applies specified function for each element of the array. Does not return anything and does not modify the array.

```ts
    const array = new Uint32Array([1, 2, 3, 4, 5])
    numbers.forEach(x => console.log(x))
    // expected output: 1 2 3 4 5
```

### `TypedArray.includes`

Returns true if provided value exists in the array, else otherwise.

```ts
    const array = new Uint32Array([1, 2, 3, 4])
    console.log(array.includes(3))
    // expected output: true
```

### `TypedArray.indexOf`

Similar to Array.findIndex, but uses equality to test elements

```ts
    const array = new Uint8Array([0, 132, 4, 221])
    const index = array.indexOf(4)
    console.log(index)
    // expected output: 2

    const neg_index = array.indexOf(42)
    console.log(neg_index)
    // expected output: -1
```

### `TypedArray.join`

Joins array elements with specified separator, using toString method on every element of array.
If no separator is provided, default separator "," (comma) is used.

```ts
    const array1 = new Uint32Array([0, 1, 2, 3])
    const joined1 = array1.join()
    console.log(joined1)
    // expected output: 0,1,2,3

    const array2 = new Float64Array([12, 7.25, 5.25, 5.255])
    const joined2 = array2.join("")
    console.log(joined2)
    // expected output: 127.255.255.255
```

### `TypedArray.keys` 

TODO: iterator

### `Array.lastIndexOf`

Array is searched backwards, starting from provided fromIndex and index of found element is returned.
If no element is found, returns -1.

```ts
    const array = new Int8Array([-1, -2, -3, 0, 0, 1])
    const index = array.indexOf(0)
    console.log(index)
    // expected output: 4

    const neg_index = array.indexOf(105)
    console.log(neg_index)
    // expected output: -1
```

### `TypedArray.map`

Creates new array, containing results of application of provided function to each element of array.

```ts
    const array = new Uint8Array([1, 2, 3, 4])
    const powers_of_two = array.map(x => 2 ** x)
    console.log(powers_of_two)
    // expected output: [2, 4, 8, 16]
```