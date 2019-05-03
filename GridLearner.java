import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.HashMap;

public class GridLearner
{
	
	public static Grid grid = new Grid();
	
	public static QTable Q;
	
	public static void main(String[] args) throws IOException
	{
		
		
		initializeQ(0);
		
		double epsilon = 0.1;
		
		double episodeRewards[] = new double[100];
		
		Writer w = new FileWriter("epsilon5.csv");
		
		BufferedWriter bw = new BufferedWriter(w);
		
		for(int i = 1; i <= 100; i++)
		{
			episodeRewards[i-1] = episode(i, epsilon, false);
			
			System.out.println(episodeRewards[i-1]);
			
			bw.write(Double.toString(episodeRewards[i-1]));
			bw.newLine();
			
		}
		
		bw.flush();
		bw.close();
		
		
		
	}
	
	public static double episode(int iteration, double epsilon, boolean softMax)
	{
		@SuppressWarnings("unused")
		QTable q = Q;
		State s = grid.generateStartState();
		
		double alpha = 1/iteration;
		double gamma = 0.9;
		
		double discountedReward = 0.0;
		
		double choiceValue = 0.0;
		
		while(!s.equals(Grid.ABSORBING_STATE))
		{	
			HashMap<String, Double> actionValues = new HashMap<String, Double>();
			
			String chosenAction;
			
			for(String action : grid.actions)
			{
				actionValues.put(action, Q.get(s, action));
			}
			
			if(softMax)
				chosenAction = softMax(actionValues);
			
			else
				chosenAction = greedyEpsilon(actionValues, epsilon);
			
			State nextState = grid.generateNextState(s, chosenAction);
				
			double r = grid.generateReward(s, chosenAction);
				
			double value = (1-alpha) * Q.get(s, chosenAction) + alpha * (r + gamma * maxExpectedNextState(nextState));
				
			Q.put(s, chosenAction, value);
			
			choiceValue = r;
			
			if(choiceValue == 1)
				System.out.println("Found Goal");
			if(choiceValue == -1)
				System.out.println("Found Hole");
			
			discountedReward *= gamma;
			discountedReward += choiceValue;
			
			s = nextState;
		}
		
		
		
		return discountedReward;
	}
	
	public static double maxExpectedNextState(State s)
	{
		
		double max = Double.NEGATIVE_INFINITY;
		
		for(String action : grid.actions)
		{
			double r = grid.generateReward(s, action);
			
			if(r > max)
				max = r;
		}
		
		return max;
	}
	
	public static void initializeQ(double initValue)
	{
		Q = new QTable(grid.states, grid.actions, initValue);
	}
	
	public static String greedyEpsilon(HashMap<String, Double> actionRewards, double epsilon)
	{	
		double rand = Math.random();
		
		//Checks to see whether rand is within the probability to choose the max value
		if(rand < 1-epsilon)
		{
			
			//Gives the argmax of the 4 actions and returns it
			String max = "";
			double maxValue = Double.NEGATIVE_INFINITY;
			
			for(String action : grid.actions)
			{
				double r = actionRewards.get(action);
				if(r > maxValue)
				{
					max = action;
					maxValue = r;
				}
			}
			
			return max;
		}
		
		//Chooses some choice at random
		int randChoice = (int) Math.floor(4*Math.random());
		
		switch(randChoice)
		{
			case 0: return "up";
			case 1: return "down";
			case 2: return "left";
			case 3: return "right";
			default: return null;
		}
	}
	
	//Softmax function takes the value of each action and randomly returns an action with
	//higher probability the more advantageous the action is
	public static String softMax(HashMap<String, Double> actionRewards)
	{
		double e = Math.E;
		
		double discount = 0.5;
		
		double upValue = actionRewards.get("up");
		double downValue = actionRewards.get("down");
		double leftValue = actionRewards.get("left");
		double rightValue = actionRewards.get("right");
		
		double upProb = 0;
		double downProb = 0;
		double leftProb = 0;
		double rightProb = 0;
		
		
		double numerator = 0;
		double denominator = 0;
		
		denominator = Math.pow(e, upValue/discount) + Math.pow(e, downValue/discount) + Math.pow(e, leftValue/discount) + Math.pow(e, rightValue/discount);
		
		upProb = Math.pow(e, upValue/discount)/denominator;
		downProb = Math.pow(e, downValue/discount)/denominator;
		leftProb = Math.pow(e, leftValue/discount)/denominator;
		rightProb = Math.pow(e, rightValue/discount)/denominator;
		
		double rand = Math.random();
		
		if(rand < upProb)
			return "up";
		else if(rand < upProb+downProb)
			return "down";
		else if(rand < upProb+downProb+leftProb)
			return "left";
		else
			return "right";
	}
	
	
}
