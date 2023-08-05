DEFAULT_CRAWL_CONFIG = {
    # Required
    'seed_urls' : [
    
    ],
    
    'collections_path' : '',

    'collection_name' : '',

    # Optional
    
    'crawl_filter_strings' : [
                        
    ],

    'crawl_required_strings' : [
    ],        
            
    'index_filter_strings' : [
        
    ],
    
    'index_required_strings' : [
                          
    ], 

    'max_redirects_per_url' : 10, 
    
    'max_tries_per_url' : 1, 
    
    'max_workers' : 5, 
    
    'max_saved_responses' : 20, 

    'login_url' : '',
    'login_data' : {},
    
    # Unimplemented 
    'max_hops' : 10
}

PRODUCTION_CRAWL_CONFIG = DEFAULT_CRAWL_CONFIG.copy()

PRODUCTION_CRAWL_CONFIG.update({
    'max_saved_responses' : 1000000000, 
    'max_hops' : 100,
    'max_workers' : 100
})
