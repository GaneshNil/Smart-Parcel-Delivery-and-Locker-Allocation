class Parcel:
    def __init__(self, parcel_id, recipient, contact, destination, weight,
                 locker=None, status="Registered", route=None):
        self.parcel_id = parcel_id
        self.recipient = recipient
        self.contact = contact
        self.destination = destination
        self.weight = weight
        self.locker = tuple(locker) if locker is not None else None
        self.status = status
        self.route = route


SAMPLE_DESTINATIONS = (
    "Kothrud", "Karve Nagar", "Deccan", "Shivajinagar", "Baner",
    "Wakad", "Hadapsar", "Viman Nagar", "Katraj", "Hinjewadi",
)

SAMPLE_NAMES = (
    "Aditi Joshi", "Rahul Sharma", "Neha Patil", "Om Kulkarni",
    "Isha Desai", "Rohan Shah", "Meera Rao", "Arjun Naik",
    "Sneha Jadhav", "Dev Mehta", "Ananya Kale", "Kunal More",
    "Riya Gokhale", "Vivek Sane", "Maya Bhosale", "Ravi Pawar",
    "Sara Inamdar", "Nikhil Shetty", "Tara Sawant", "Aman Sethi",
)


def sample_parcels():
    parcels = []
    for index, recipient in enumerate(SAMPLE_NAMES):
        parcels.append(Parcel(
            f"P{101 + index}", recipient, f"000000{index + 1:04}",
            SAMPLE_DESTINATIONS[index % len(SAMPLE_DESTINATIONS)],
            0.5 + (index % 10) * 0.25,
        ))
    return parcels
