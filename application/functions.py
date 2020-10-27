def status_rename(string):
    status = {
        'pausedUP' : 'Complete',
        'stalledUP' : 'Seeding (Idle)',
        'uploading' : 'Seeding',
        'forcedUP': 'Seeding (f)',
        'queuedUP' : 'Queued',
        'queuedDL' : 'Queued',
        'checkingUP' : 'Checking',
        'downloading' : 'Downloading',
        'forceDL' : 'Downloading (f)',
        'metaDL' : 'Fetching Metadata',
        'pausedDL' : 'Paused',
        'stalledDL' : 'Stalled',
        'checkingDL' : 'Checking',
        'checkingResumeData' : 'Checking',
    }

    if string in status.keys():
        string = status[string]

    return string

