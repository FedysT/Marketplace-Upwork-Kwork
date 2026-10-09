from django.db import migrations

def seed_categories(apps, schema_editor):
    Category = apps.get_model("services", "Category")
    categories = [
        ("Programming & Tech", "programming-tech", "Websites, apps, automation and code."),
        ("Design & Creative", "design-creative", "Logos, graphics, UI and visual design."),
        ("Writing & Translation", "writing-translation", "Articles, copywriting, translation and editing."),
        ("Video & Animation", "video-animation", "Editing, motion graphics and short-form video."),
        ("Digital Marketing", "digital-marketing", "SEO, social media and growth services."),
        ("Business", "business", "Research, consulting, presentations and support."),
    ]
    Category.objects.bulk_create([
        Category(name=name, slug=slug, description=description)
        for name, slug, description in categories
    ])

class Migration(migrations.Migration):
    dependencies = [("services", "0001_initial")]
    operations = [migrations.RunPython(seed_categories, migrations.RunPython.noop)]
