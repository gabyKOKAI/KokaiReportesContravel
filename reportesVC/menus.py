from menu import Menu, MenuItem
from django.urls import reverse

# Define children for reports
reportes_children = (
    MenuItem("Reportes Comisiones",
             reverse('reportesVC:reportes', kwargs={'tipoNombre': 'Comisiones', 'status': 'Nuevo'}),
             weight=20,
             icon="report",
             separator=True),
    MenuItem("Reportes Ventas",
             reverse('reportesVC:reportes', kwargs={'tipoNombre': 'Ventas', 'status': 'Nuevo'}),
             weight=20,
             icon="report",
             separator=True),
)

# Add two items to our main menu
Menu.add_item("main", MenuItem("Inicio",
                               reverse('reportesVC:index'),
                               weight=10,
                               icon="tools",
                               separator=True))

Menu.add_item("main", MenuItem("Reportes",
                               "#",
                               weight=20,
                               children=reportes_children,
                               icon="report",
                               separator=True))

'''Menu.add_item("main", MenuItem("Inicio2",
                               "#1",
                               weight=30,
                               icon="tools",
                               separator=True))

Menu.add_item("main", MenuItem("Reportes2",
                               "#",
                               weight=40,
                               children=reportes_children,
                               icon="report",
                               separator=True))
'''

'''
# Define children for the my account menu
myaccount_children = (
    MenuItem("Edit Profile",
             reverse("accounts.views.editprofile"),
             weight=10,
             icon="user"),
    MenuItem("Admin",
             reverse("admin:index"),
             weight=80,
             separator=True,
             check=lambda request: request.user.is_superuser),
    MenuItem("Logout",
             reverse("accounts.views.logout"),
             weight=90,
             separator=True,
             icon="user"),
)

# Add a My Account item to our user menu
Menu.add_item("user", MenuItem("My Account",
                               reverse("accounts.views.myaccount"),
                               weight=10,
                               children=myaccount_children))
'''