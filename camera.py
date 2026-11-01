def covers_light(light_ranges, need_min, need_max):
    """Do these light ranges cover need_min..need_max with no gap?"""
    reach = need_min
    for lo, hi in sorted(light_ranges):
        if lo > reach:          # gap
            break
        reach = max(reach, hi)
        if reach >= need_max:
            return True
    return False


def can_cover(need_dist, need_light, cameras):
    """
    need_dist  = (min_distance, max_distance)
    need_light = (min_light, max_light)
    cameras    = list of (dist_min, dist_max, light_min, light_max)
    """
    d_min, d_max = need_dist
    l_min, l_max = need_light

    # 1. All distances where something changes
    edges = {d_min, d_max}
    for dmin, dmax, _, _ in cameras:
        for d in (dmin, dmax):
            if d_min <= d <= d_max:
                edges.add(d)
    edges = sorted(edges)

    # 2. Test every edge and every spot between two edges
    test_points = list(edges)
    for a, b in zip(edges, edges[1:]):
        test_points.append((a + b) / 2)

    # 3. At each test distance, the light ranges must have no gap
    for x in test_points:
        lights = [(lmin, lmax)
                  for dmin, dmax, lmin, lmax in cameras
                  if dmin <= x <= dmax]
        if not covers_light(lights, l_min, l_max):
            return False
    return True


# ---------- tests ----------
need_d, need_l = (1, 10), (1, 10)

print(can_cover(need_d, need_l, [(0, 20, 0, 20)]))                 # True
print(can_cover(need_d, need_l, [(1, 5, 1, 10), (5, 10, 1, 10)]))  # True
print(can_cover(need_d, need_l, [(1, 5, 1, 10), (5, 10, 1, 5)]))   # False (gap top right)
print(can_cover(need_d, need_l, [(1, 5, 1, 10), (6, 10, 1, 10)]))  # False (gap 5 to 6)
print(can_cover(need_d, need_l, []))                               # False