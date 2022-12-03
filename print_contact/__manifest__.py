{
        'name':'Printing of contacts',
        'description':'Provide contacts pdfs reports',
        'summary':'Many PDFs available for provide contacts reports.',
        'author':'Yvan Dotet',
        'depends':['base','contacts'],
        'application':False,        
        'version':'15.0.1.0.0',
        'license':'AGPL-3',
        'support': 'yvandotet@yahoo.fr',
        'website':'https://github.com/YvanDotet/print_contact',
        
        'data':[
            'views/print_buttons.xml',
            
            'report/print_page.xml',
            'report/print_listing.xml',
            'report/print_checkin.xml',
            ],
         
        'images': ['images/thumbnail.png'],
}

