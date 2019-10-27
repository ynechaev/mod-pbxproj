def is_in_save(current_obj):
    return _get_save_caches(current_obj) is not None


def get_from_cache_during_save(current_obj, caches_key_type, caches_key_obj, fill_cache_func, target_key):
    save_caches = _get_save_caches(current_obj)
    assert save_caches is not None, 'Must only call this during a save operation!'
    cache_key = (caches_key_type, id(caches_key_obj))
    cache = save_caches.get(cache_key)
    if cache is None:
        cache = {}
        fill_cache_func(cache)
        save_caches[cache_key] = cache
    return cache.get(target_key)


def _get_save_caches(current_obj):
    # Lazy import to break circular dependency
    from pbxproj.XcodeProject import XcodeProject

    root_project = current_obj
    while root_project is not None and not isinstance(root_project, XcodeProject):
        root_project = root_project.get_parent()
    if root_project is None:
        return None
    return root_project._save_caches
