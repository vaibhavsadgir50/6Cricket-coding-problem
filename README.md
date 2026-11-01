# Software Camera Coverage (Python)

Decide whether a set of hardware cameras can together act as one "software camera" that handles every required subject distance and light level.

## Problem

Each hardware camera works well for a range of subject distances and a range of light levels. The software camera picks a suitable hardware camera for every shot. Given:

- the distance range and light range the software camera must support, and
- a list of hardware cameras with their own distance and light ranges,

return `True` if every possible (distance, light) combination is handled by at least one camera, otherwise `False`.

## Files

| File | Purpose |
|---|---|
| `camera.py` | The solution and a few test cases. Pure Python, no third-party libraries. |
| `README.md` | This document. |

## How to run

```bash
python camera.py
```

Expected output:

```
True
True
False
False
False
```

## Usage

```python
from camera import can_cover

need_distance = (1, 10)     # (min_distance, max_distance)
need_light    = (1, 10)     # (min_light, max_light)

cameras = [
    # (dist_min, dist_max, light_min, light_max)
    (1, 5, 1, 10),
    (5, 10, 1, 10),
]

print(can_cover(need_distance, need_light, cameras))   # True
```

## Assumptions

- All ranges are **closed** (both ends included). A camera ending at distance 5 and another starting at 5 leave no gap.
- Cameras may overlap each other and may extend beyond the required range.
- Ranges are independent: a camera works for any distance in its range combined with any light level in its range.
- Every range satisfies `min <= max`.

## Approach

Think of a graph with distance on the horizontal axis and light level on the vertical axis.

- Every shot is a **dot**.
- Every hardware camera covers a **rectangle** of dots (its distance range times its light range).
- The software camera is a **target rectangle**.
- The question becomes: do the camera rectangles together cover the target rectangle with no hole?

Steps:

1. **Find where things change.** Collect the start and end distance of each camera (only those inside the target range) plus the target's own start and end. These are the only distances where the set of usable cameras can change.
2. **Pick test points.** Test every one of those edge distances, plus the midpoint between each pair of neighbouring edges. Between two neighbouring edges the same cameras are active, so one midpoint represents the whole strip.
3. **Reduce to 1D.** At each test distance, keep only the cameras whose distance range contains it. Their light ranges must cover the needed light range.
4. **Greedy interval cover.** Sort the light ranges by start. Keep a `reach` pointer. If a range starts after `reach`, there is a gap, so fail. Otherwise extend `reach` to the largest end seen. Succeed once `reach` passes the needed maximum.
5. If every test distance passes, return `True`. If any fails, return `False`.

DSA concepts used: interval coverage, dimension reduction (2D to 1D), coordinate compression, sorting, greedy sweep.

## Complexity

- **Time:** O(n² log n). There are O(n) test points, and each needs an O(n) filter and an O(n log n) sort.
- **Space:** O(n).

## Test cases included

| Case | Expected |
|---|---|
| One camera larger than the target | `True` |
| Two cameras side by side, touching at distance 5 | `True` |
| Gap in the top-right corner | `False` |
| Real gap between distances 5 and 6 | `False` |
| No cameras | `False` |

