int getMovingAverage(byte newValue) {
  const int BUFFER_SIZE = 10;
  static byte buffer[BUFFER_SIZE] = {0};
  static int index = 0;
  static int total = 0;
  static int count = 0;

  // Subtract the oldest value
  total -= buffer[index];

  // Store new value
  buffer[index] = newValue;
  total += newValue;

  // Update index
  index = (index + 1) % BUFFER_SIZE;

  // Update count (max: BUFFER_SIZE)
  if (count < BUFFER_SIZE) count++;

  // Return average as byte
  return (int)(total / count);
}
