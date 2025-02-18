def watchlist_count(request):
    if request.user.is_authenticated:
        return {'watchlist_count': request.user.watchlist.count()}
    return {'watchlist_count': 0}
