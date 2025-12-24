import os
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from pytz import timezone as pytz_timezone
import pytz

def load_all_events(events_dir='events'):
    """Load all YAML files from events directory"""
    all_events = []
    events_path = Path(events_dir)
    
    yaml_files = sorted(events_path.glob('**/*.yaml'))
    
    for yaml_file in yaml_files:
        # Skip template files
        if 'TEMPLATE' in yaml_file.name.upper() or yaml_file.suffix == '.example':
            print(f"Skipping template: {yaml_file}")
            continue
            
        print(f"Loading {yaml_file}")
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if data:
                # Support both formats:
                # 1. List at top level: [event1, event2, ...]
                # 2. Dict with events key: {events: [event1, event2, ...]}
                if isinstance(data, list):
                    all_events.extend(data)
                elif isinstance(data, dict) and 'events' in data:
                    all_events.extend(data['events'])
    
    return all_events

def create_datetime(date_str, time_str='00:00:00', tz_str='UTC'):
    """Create timezone-aware datetime from strings"""
    dt_str = f"{date_str} {time_str}"
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    tz = pytz_timezone(tz_str)
    return tz.localize(dt)

def create_race_event(event_data):
    """Create iCalendar event for the race day"""
    cal_event = Event()
    
    # Basic info
    event_id = event_data['id']
    cal_event.add('uid', f"{event_id}@marathon-calendar.com")
    cal_event.add('dtstamp', datetime.now(pytz.utc))
    
    # Race date and time
    race_dt = create_datetime(
        event_data['date'],
        event_data.get('time', '09:00:00'),
        event_data.get('timezone', 'UTC')
    )
    cal_event.add('dtstart', race_dt)
    
    # Estimate 6 hours for marathon duration
    cal_event.add('dtend', race_dt + timedelta(hours=6))
    
    # Name
    cal_event.add('summary', f"🏃 {event_data['name']}")
    
    # Build description
    description_parts = []
    
    if 'details' in event_data and 'description' in event_data['details']:
        description_parts.append(event_data['details']['description'].strip())
        description_parts.append('')
    
    # Add categories info if exists
    if 'categories' in event_data:
        description_parts.append('竞赛项目 (Race Categories):')
        for cat in event_data['categories']:
            unit = cat.get('distance_unit', 'km')
            capacity = cat.get('capacity', 'N/A')
            description_parts.append(
                f"• {cat['name']}: {cat['distance']}{unit} - {capacity}人"
            )
        description_parts.append('')
    
    # Registration info
    if 'registration' in event_data:
        reg = event_data['registration']
        description_parts.append('报名信息 (Registration):')
        description_parts.append(f"Opens: {reg.get('open_date', reg.get('opens', 'N/A'))}")
        description_parts.append(f"Closes: {reg.get('close_date', reg.get('closes', 'N/A'))}")
        
        if 'lottery_date' in reg:
            description_parts.append(f"Lottery Results: {reg['lottery_date']}")
        
        description_parts.append(f"URL: {reg['url']}")
        
        if 'cost' in reg:
            cost_info = []
            if isinstance(reg['cost'], dict):
                for key, value in reg['cost'].items():
                    cost_info.append(f"{key.title()}: {value}")
            else:
                cost_info.append(str(reg['cost']))
            description_parts.append(f"Cost: {', '.join(cost_info)}")
        
        if 'requirements' in reg:
            description_parts.append('\nRequirements:')
            for req in reg['requirements']:
                description_parts.append(f"  • {req}")
        
        if 'packet_pickup' in reg:
            pickup = reg['packet_pickup']
            description_parts.append(
                f"\nPacket Pickup: {pickup['start']} to {pickup['end']}"
            )
            if 'note' in pickup:
                description_parts.append(f"  {pickup['note']}")
        
        description_parts.append('')
    
    # Contact info
    if 'details' in event_data and 'contact' in event_data['details']:
        contact = event_data['details']['contact']
        description_parts.append('联系方式 (Contact):')
        if 'wechat' in contact:
            description_parts.append(f"WeChat: {contact['wechat']}")
        if 'email' in contact:
            description_parts.append(f"Email: {contact['email']}")
        if 'website' in event_data['details']:
            description_parts.append(f"Website: {event_data['details']['website']}")
    
    cal_event.add('description', '\n'.join(description_parts))
    
    # Location
    if 'location' in event_data:
        loc = event_data['location']
        location_str = f"{loc.get('venue', '')}, {loc.get('city', '')}, "
        if 'state' in loc:
            location_str += f"{loc['state']}, "
        location_str += loc.get('country', '')
        cal_event.add('location', location_str.strip(', '))
        
        # Geo coordinates
        if 'coordinates' in loc:
            coords = loc['coordinates']
            cal_event.add('geo', (coords['lat'], coords['lon']))
    
    # URL
    if 'details' in event_data and 'website' in event_data['details']:
        cal_event.add('url', event_data['details']['website'])
    
    # Categories/Tags
    if 'tags' in event_data:
        cal_event.add('categories', event_data['tags'])
    
    # Status
    status = event_data.get('status', 'confirmed').upper()
    cal_event.add('status', status)
    
    return cal_event

def create_registration_event(event_data):
    """Create iCalendar event for registration window"""
    if 'registration' not in event_data:
        return None
    
    reg = event_data['registration']
    cal_event = Event()
    
    # Basic info
    event_id = event_data['id']
    cal_event.add('uid', f"{event_id}-registration@marathon-calendar.com")
    cal_event.add('dtstamp', datetime.now(pytz.utc))
    
    # Registration window dates
    opens_dt = create_datetime(
        reg.get('open_date', reg.get('opens')),
        reg.get('open_time', reg.get('opens_time', '00:00:00')),
        event_data.get('timezone', 'UTC')
    )
    closes_dt = create_datetime(
        reg.get('close_date', reg.get('closes')),
        reg.get('close_time', reg.get('closes_time', '23:59:59')),
        event_data.get('timezone', 'UTC')
    )
    
    cal_event.add('dtstart', opens_dt)
    cal_event.add('dtend', closes_dt)
    
    # Name
    cal_event.add('summary', f"📝 {event_data['name']} - 报名 (Registration)")
    
    # Description
    description_parts = [
        f"{event_data['name']} 报名窗口期",
        f"{event_data['name']} Registration Window",
        f"\n比赛日期 (Race Date): {event_data['date']}",
        f"\n报名网址 (Registration URL): {reg['url']}",
    ]
    
    if 'lottery_date' in reg:
        description_parts.append(f"抽签结果公布 (Lottery Results): {reg['lottery_date']}")
    
    if 'cost' in reg:
        description_parts.append('\n费用 (Cost):')
        if isinstance(reg['cost'], dict):
            for key, value in reg['cost'].items():
                description_parts.append(f"  • {key.title()}: {value}")
        else:
            description_parts.append(f"  {reg['cost']}")
    
    if 'requirements' in reg:
        description_parts.append('\n要求 (Requirements):')
        for req in reg['requirements']:
            description_parts.append(f"  • {req}")
    
    if 'packet_pickup' in reg:
        pickup = reg['packet_pickup']
        description_parts.append(
            f"\n领物时间 (Packet Pickup): {pickup['start']} - {pickup['end']}"
        )
        if 'note' in pickup:
            description_parts.append(f"  {pickup['note']}")
    
    # Contact info
    if 'details' in event_data and 'contact' in event_data['details']:
        contact = event_data['details']['contact']
        description_parts.append('\n联系方式 (Contact):')
        if 'wechat' in contact:
            description_parts.append(f"  WeChat: {contact['wechat']}")
        if 'email' in contact:
            description_parts.append(f"  Email: {contact['email']}")
    
    cal_event.add('description', '\n'.join(description_parts))
    
    # URL
    cal_event.add('url', reg['url'])
    
    # Location (city level for registration)
    if 'location' in event_data:
        loc = event_data['location']
        location_parts = [loc.get('city', '')]
        if 'state' in loc:
            location_parts.append(loc['state'])
        location_parts.append(loc.get('country', ''))
        cal_event.add('location', ', '.join(filter(None, location_parts)))
    
    # Categories
    cal_event.add('categories', ['Registration', 'Deadline'])
    
    # Status
    cal_event.add('status', 'CONFIRMED')
    
    return cal_event

def generate_calendar(output_file='output/china.ics'):
    """Generate the complete iCalendar file"""
    
    # Create calendar
    cal = Calendar()
    cal.add('prodid', '-//Marathon Calendar//marathon-calendar.com//')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'Marathon Events Calendar')
    cal.add('x-wr-timezone', 'UTC')
    cal.add('x-wr-caldesc', 
            'Marathon races worldwide with registration windows')
    
    # Load all events from YAML
    events = load_all_events()
    print(f"\nLoaded {len(events)} marathon events from YAML files")
    
    # Generate calendar events
    total_calendar_events = 0
    for event_data in events:
        print(f"\nProcessing: {event_data['name']}")
        
        # Create race day event
        race_event = create_race_event(event_data)
        cal.add_component(race_event)
        total_calendar_events += 1
        print(f"  ✓ Created race event")
        
        # Create registration window event
        reg_event = create_registration_event(event_data)
        if reg_event:
            cal.add_component(reg_event)
            total_calendar_events += 1
            print(f"  ✓ Created registration event")
    
    # Write to file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'wb') as f:
        f.write(cal.to_ical())
    
    print(f"\n{'='*60}")
    print(f"✅ Calendar generated successfully!")
    print(f"{'='*60}")
    print(f"Output file: {output_file}")
    print(f"YAML events: {len(events)}")
    print(f"Calendar events (VEVENT): {total_calendar_events}")
    print(f"{'='*60}")

if __name__ == '__main__':
    generate_calendar()
