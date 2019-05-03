import java.util.HashMap;
import java.util.List;

public class QTable
{
	public HashMap<State, HashMap<String, Double>> table;
	
	public QTable(List<State> states, List<String> actions, double initValue)
	{
		
		table = new HashMap<State, HashMap<String, Double>>();
		
		for(State s : states)
		{
			
			table.put(s, new HashMap<String, Double>());
			
			for(String action : actions)
			{
				this.put(s, action, initValue);
			}
		}
	}
	
	
	public void put(State s, String action, double value)
	{
		table.get(s).put(action, value);
	}
	
	public double get(State s, String action)
	{
		return table.get(s).get(action);
	}
	
	public HashMap<String, Double> getActionValues(State s)
	{
		return table.get(s);
	}
	
	
}
