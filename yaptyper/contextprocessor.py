def canonical_url(request):
    path = request.path
    canonical_domain = "https://yaptyper.ovh"
    return {
        "canonical_url": f"{canonical_domain}{path}"
    }