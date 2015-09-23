from datetime import datetime

time = datetime.now().strftime('%A %B %d, %Y - %I:%M %p')

print time

log_text = '''
        Added %d clean URLs to all_urls.txt
        Removed %d bad URLs from all_urls.txt
        Added %d clean URLs to animals_urls.txt
        Removed %d bad URLs from animals_urls.txt
        Added %d clean URLs to gaming_urls.txt
        Removed %d bad URLs from gaming_urls.txt
        Added %d clean URLs to strange_urls.txt
        Removed %d bad URLs from strange_urls.txt
        Added %d clean URLs to educational_urls.txt
        Removed %d bad URLs from educational_urls.txt
        ''' % (self.clean_urls_all, self.bad_urls_all, self.clean_urls_animals,
               self.bad_urls_animals, self.clean_urls_gaming, self.bad_urls_gaming,
               self.clean_urls_strange, self.bad_urls_strange, self.clean_urls_educational,
               self.bad_urls_educational)