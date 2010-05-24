Introduction
============

If items are at the same level in a folder then they will be sorted based on a
'_sortorder' key as given by transmogrify.webcrawler.

In addition

- if an item doesn't exist for a given items parent it will be created. The _type key will
  be set to the first item in 'default_containers'.

- if a container has a 'text' key then a default page will be created.

- if item's name is in 'default_pages' and it's parent doesn't already have a defaultpage
  then the item will be set as the parents default page.