import { MeetingSimulator } from "@/components/meeting/meeting-simulator";
import { LiveMeeting } from "@/components/meeting/live-meeting";

export default function MeetingPage() {
  return (
    <div className="space-y-12 pb-12">
      <LiveMeeting />
      <MeetingSimulator />
    </div>
  );
}
